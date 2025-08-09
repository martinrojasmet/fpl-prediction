import prisma from "../prisma/prisma-client.js";

export const getDoubleGws = async (filters = {}, cursor, limit) => {
    const cursorObj = cursor ? { id: parseInt(cursor, 10) } : undefined;
    const takeLimit = limit ? parseInt(limit, 10) : 50;
    try {
        const doubleGW = await prisma.doubleGW.findMany({
            where: filters,
            take: takeLimit,
            ...(cursorObj && { cursor: cursorObj }),
            skip: cursorObj ? 1 : 0,
            orderBy: { id: 'asc' }
        });
        const nextCursor = doubleGW.length === takeLimit ? doubleGW[doubleGW.length - 1].id : null;
        return {
            data: doubleGW,
            nextCursor
        };
    } catch (error) {
        throw new Error("Error retrieving double gameweeks: " + error.message);
    }
};

export const getDoubleGwByGw = async (gw) => {
    try {
        const doubleGW = await prisma.doubleGW.findMany({
            where: { gw: parseInt(gw, 10) },
        });
        return doubleGW;
    } catch (error) {
        throw new Error("Error retrieving double gameweek: " + error.message);
    }
};

export const createDoubleGws = async (doubleGwsData) => {
    try {
        const doubleGW = await prisma.doubleGW.createMany({
            data: doubleGwsData
        });
        return doubleGW;
    } catch (error) {
        throw new Error("Error creating double gameweeks: " + error.message);
    }
};

export const updateDoubleGw = async (id, doubleGwData) => {
    try {
        const doubleGW = await prisma.doubleGW.update({
            where: { id: parseInt(id, 10) },
            data: doubleGwData
        });
        return doubleGW;
    } catch (error) {
        throw new Error("Error updating double gameweek: " + error.message);
    }
};

export const deleteDoubleGw = async (id) => {
    try {
        const doubleGW = await prisma.doubleGW.delete({
            where: { id: parseInt(id, 10) },
        });
        return doubleGW;
    } catch (error) {
        throw new Error("Error deleting double gameweek: " + error.message);
    }
};