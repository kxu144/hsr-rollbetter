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

    const [improveP, setImproveP] = useState(null);
    useEffect(() => {
        if (p.length > 0) {
            let farmP1 = 0;
            let farmP2 = 0;
            let craftP = 0;
            for (let i = 0; i < p.length; i++) {
                craftP = Math.max(craftP, p[i]['mainstat'] * p[i]['substat']); // improve char by crafting is just max probability
                if (i < 4) {
                    farmP1 += 0.125 * p[i]['mainstat'] * p[i]['substat']; // 0.5 * 0.25 for right set + right type
                } else {
                    farmP2 += 0.25 * p[i]['mainstat'] * p[i]['substat']; // 0.5 * 0.5
                }
            }
            setImproveP([Math.max(farmP1, farmP2), craftP]);
        }
    }, [p])

    return (
        <div>
            E{data['eidolons']} {data['name']}
            {data['relics'].map((e, i) => {
                return <Relic key={i} relic={e} p={i < p.length ? p[i] : undefined}/>;
            })}
            {improveP && `Probability of farming improvement: ${improveP[0]}`}
            {improveP && `Probability of crafting improvement: ${improveP[1]}`}
        </div>
    )
}

export default CharCard;