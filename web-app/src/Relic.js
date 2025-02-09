import { useEffect, useState } from "react";

function Relic({ relic }) {
    const [p, setP] = useState(0);
    useEffect(() => {
        const getP = async () => {
            const response = await fetch(`http://localhost:5000/relic`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(relic),
            })

            const data = await response.json();
            setP(data['mainstat'] * data['substat']);
        };

        if (relic) {
            getP();
        }
    }, [relic]);

    return (
        <div style={{border: '1px solid black'}}>
            {relic['type']}
            {relic['main_stat']['name']} {relic['main_stat']['value']}
            {relic['sub_stats'].map((e, i) => {
                return <div key={i}>{e['name']} {e['value']}</div>;
            })}
            Probability of better: {Math.floor(p*1e4) / 100}%
        </div>
    )
}

export default Relic;