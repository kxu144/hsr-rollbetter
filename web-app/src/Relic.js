function Relic({ relic }) {
    return (
        <div style={{border: '1px solid black'}}>
            {relic['type']}
            {relic['main_stat']['name']} {relic['main_stat']['value']}
            {relic['sub_stats'].map((e, i) => {
                return <div>{e['name']} {e['value']}</div>;
            })}
        </div>
    )
}

export default Relic;