import { create } from 'zustand';

export type Game = {
  id: number;
  title: string;
  image: string;
  owned: boolean;
};

type State = {
  games: Map<string, Game>;
};
type Actions = {
  fetchGames: () => Promise<void>;
  // updateGame: () => Promise<Game>
};

export const useGameStore = create<State & Actions>()((set) => ({
  games: new Map<string, Game>(),
  fetchGames: async () => {
    const response = await fetch('http://127.0.0.1:8000/api/games', {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        'content-type': 'application/json',
      },
    });
    if (response.ok) {
      const gamesArray = await response.json();
      set({
        games: new Map<string, Game>(
          gamesArray.map((game: Game) => [game.id.toString(), game]),
        ),
      });
    }
  },
}));
