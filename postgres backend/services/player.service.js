import prisma from "../prisma/prisma-client.js";

export const getPlayers = async (filters = {}, cursor, limit) => {
    const cursorObj = cursor ? { id: parseInt(cursor, 10) } : undefined;
    let takeLimit = parseInt(limit, 10);
    if (!takeLimit || isNaN(takeLimit)) {
        takeLimit = 50;
    }

    try {
        const players = await prisma.player.findMany({
            where: filters,
            take: takeLimit,
            ...(cursorObj && { cursor: cursorObj }),
            skip: cursorObj ? 1 : 0,
            orderBy: { id: 'asc' }
        });
        const nextCursor = players.length === takeLimit ? players[players.length - 1].id : null;
        return {
            data: players,
            nextCursor
        };
    } catch (error) {
        throw new Error("Error retrieving players: " + error.message);
    }
}

export const getPlayersFPLNames = async () => {
    try {
        const players = await prisma.player.findMany({
            select: {
                fpl_name: true
            },
        });

        return players.map(player => player.fpl_name);
    } catch (error) {
        throw new Error("Error retrieving players: " + error.message);
    }
}

export const getPlayersUnderstatNames = async () => {
    try {
        const players = await prisma.player.findMany({
            select: {
                understat_name: true
            },
        });

        return [...new Set(players
            .map(player => player.understat_name)
            .filter(name => name !== ""))];
    } catch (error) {
        throw new Error("Error retrieving players: " + error.message);
    }
}

export const createPlayers = async (playersData) => {
    try {
        const players = await prisma.player.createMany({
            data: playersData
        });
        return players;
    } catch (error) {
        throw new Error("Error creating players: " + error.message);
    }
}

export const updatePlayersUnderstatNames = async (body) => {
    try {
        const fplName = body.fpl_name;
        const newUnderstatName = body.understat_name;

        const players = await prisma.player.updateMany({
            where: {
                fpl_name: fplName,
            },
            data: {
                understat_name: newUnderstatName,
            },
        });
        return players;
    } catch (error) {
        throw new Error("Error updating players: " + error.message);
    }
}

export const deletePlayerByFPLName = async (fplName) => {
    try {
        const players = await prisma.player.deleteMany({
            where: {
                fpl_name: fplName,
            },
        });
        return players;
    } catch (error) {
        throw new Error("Error deleting players: " + error.message);
    }
}