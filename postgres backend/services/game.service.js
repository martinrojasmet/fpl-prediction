import prisma from "../prisma/prisma-client.js";

export const getAllGames = async () => {
    try {
        const games = await prisma.game.findMany();
        return games;
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