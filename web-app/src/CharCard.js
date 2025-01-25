import { useContext } from "react";
import { useCharMap } from "./App";
import Relic from "./Relic";

function CharCard({ data }) {
    const charMap = useCharMap();
    return (
        <div>
            E{data['eidolons']} {data['name']}
            {data['relics'].map((e, i) => {
                return <Relic key={i} relic={e}/>;
            })}
        </div>
    )
}

export default CharCard;