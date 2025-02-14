import { useEffect, useState } from "react";

function Relic({ relic, p }) {


    return (
        <div style={{border: '1px solid black'}}>
            {relic['type']}
            {relic['main_stat']['name']} {relic['main_stat']['value']}
            {relic['sub_stats'].map((e, i) => {
                return <div key={i}>{e['name']} {e['value']}</div>;
            })}
            Probability of better: {p ? Math.floor(p['mainstat'] * p['substat'] * 1e4) / 100 : "NaN"}%
        </div>
    )
}

export default Relic;