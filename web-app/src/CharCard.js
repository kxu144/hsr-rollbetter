import { useContext } from "react";
import { useCharMap } from "./App";

function CharCard({ data }) {
    const charMap = useCharMap();
    return (
        <div>
            E{data['eidolons']} {data['name']}
            
        </div>
    )
}

export default CharCard;