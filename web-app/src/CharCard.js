import { useContext, useEffect, useState } from "react";
import { useCharMap } from "./App";
import Relic from "./Relic";

function CharCard({ data }) {
    const charMap = useCharMap();

    const [p, setP] = useState([]);
    useEffect(() => {
        const getP = async () => {
            const response = await fetch(`http://localhost:5001/relics`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'relics': data['relics'],
                })
            })

            const ps = await response.json();
            setP(ps);
            console.log(ps);
        };

        if (data?.relics) {
            getP();
        }
    }, [data]);


    return (
        <div>
            E{data['eidolons']} {data['name']}
            {data['relics'].map((e, i) => {
                return <Relic key={i} relic={e} p={i < p.length ? p[i] : undefined}/>;
            })}
        </div>
    )
}

export default CharCard;