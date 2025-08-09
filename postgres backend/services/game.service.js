import prisma from "../prisma/prisma-client.js";

export const getGames = async (filters = {}, cursor, limit) => {
    const cursorObj = cursor ? { id: parseInt(cursor, 10) } : undefined;
    const takeLimit = limit ? parseInt(limit, 10) : 50;
    try {
        const games = await prisma.game.findMany({
            where: filters,
            take: takeLimit,
            ...(cursorObj && { cursor: cursorObj }),
            skip: cursorObj ? 1 : 0,
            orderBy: { id: 'asc' }
        });
        const nextCursor = games.length === takeLimit ? games[games.length - 1].id : null;
        return {
            data: games,
            nextCursor
        };
    } catch (error) {
        throw new Error("Error retrieving games: " + error.message);
    }
}

export const createGames = async (gamesData) => {
    console.log("Creating games with data:", gamesData);
    try {
        const games = await prisma.game.createMany({
            data: gamesData,
        });
        return games;
    } catch (error) {
        throw new Error("Error creating games: " + error.message);
    }
}

export const getGameById = async (gameId) => {
    try {
        const game = await prisma.game.findUnique({
            where: { id: parseInt(gameId, 10) },
        });
        return game;
    } catch (error) {
        throw new Error("Error retrieving game: " + error.message);
    }
}

export const deleteGame = async (gameId) => {
    try {
        const game = await prisma.game.delete({
            where: { id: gameId },
        });
        return game;
    } catch (error) {
        throw new Error("Error deleting game: " + error.message);
    }
}