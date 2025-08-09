import prisma from "../prisma/prisma-client.js";

export const getPredictions = async (filters = {}, cursor, limit) => {
    const cursorObj = cursor ? { id: parseInt(cursor, 10) } : undefined;
    const takeLimit = limit ? parseInt(limit, 10) : 50;
    try {
        const predictions = await prisma.prediction.findMany({
            where: filters,
            take: takeLimit,
            ...(cursorObj && { cursor: cursorObj }),
            skip: cursorObj ? 1 : 0,
            orderBy: { id: 'asc' }
        });
        const nextCursor = predictions.length === takeLimit ? predictions[predictions.length - 1].id : null;
        return {
            data: predictions,
            nextCursor
        };
    } catch (error) {
        throw new Error("Error retrieving predictions: " + error.message);
    }
}

export const createPredictions = async (predictionsData) => {
    try {
        const predictions = await prisma.prediction.createMany({
            data: predictionsData,
        });
        return predictions;
    } catch (error) {
        throw new Error("Error creating prediction: " + error.message);
    }
}

