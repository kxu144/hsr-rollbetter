import React, { createContext, useContext, useEffect, useRef, useState } from 'react';
import './App.css';

import CharCard from './CharCard';



function App() {

  var [charMap, setCharMap] = useState({});
  useEffect(() => {
    const getCharMap = async () => {
      const response = await fetch('https://raw.githubusercontent.com/EnkaNetwork/API-docs/master/store/hsr/honker_characters.json');
      const result = await response.json();
      setCharMap(result);
      console.log("got charmap");
    };

    if (charMap === undefined) {
      getCharMap();
    }
  }, [charMap]);



  var [uid, setUID] = useState();
  var uidRef = useRef(null);


  var [enka, setEnka] = useState();
  useEffect(() => {
    const sendRequest = async (uid) => {
      try {
        const response = await fetch(`http://localhost:5001/enka/${uid}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        setEnka(data);
        console.log('Response from server:', data);
      } catch (error) {
        console.error('Error while fetching data:', error);
      }
    };

    // Fire the request when the page is loaded
    if (uid) {
      sendRequest(parseInt(uid));
    }
  }, [uid]); // Empty dependency array ensures this runs only once when the component mounts



  return (
    <div className="App">
      <input ref={uidRef} type='number' min='0' step='1' value={uid} placeholder='600736233'/>
      <button onClick={(e) => setUID(e.target.value || uidRef.current.placeholder)}>Enter</button>
      <CharContext.Provider value={charMap}>
        {enka && enka['characters_details'].map((e, i) => {
          if (i == 0) {
            return <CharCard key={i} data={e}/>;
          }
        })}
      </CharContext.Provider>
    </div>
  );
}

const CharContext = createContext(null);
export const useCharMap = () => {
  const context = useContext(CharContext);
  if (!context) {
    throw new Error('not in correct context');
  }
  return context;
}

export default App;
