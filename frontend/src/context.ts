import { createContext, useContext } from "react";

export const gameweekContext = createContext<number | undefined>(undefined)

export function useGameweekContext() {
    const gameweek = useContext(gameweekContext)

    if (gameweek === undefined) {
        throw new Error('useGameweekContext does not wrap the component')
    }

    return gameweek
}