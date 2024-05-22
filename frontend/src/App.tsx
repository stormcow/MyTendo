import { useEffect, useState } from 'react';
import './App.css';
import { useGameStore } from './GameStore';

function App() {
  const [games, fetchGames] = useGameStore((state) => [state.games, state.fetchGames]);
  const [fetching, setFetching] = useState(true);

  useEffect(() => {
    if (games.size !== 0) setFetching(false);
  }, [games]);
  return (
    <>
      <div className="container">
        {fetching ? (
          <button onClick={async () => await fetchGames()}>Get Games</button>
        ) : (
          // eslint-disable-next-line @typescript-eslint/no-unused-vars
          Array.from(games).map(([_, game], index) => {
            console.log(game);
            return (
              <img
                key={index}
                src={game?.image}
                className='logo card'
                onClick={()=>console.log(game)}
              />
            );
          })
        )}
      </div>
    </>
  );
}

export default App;
