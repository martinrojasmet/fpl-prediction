import prisma from "../prisma/prisma-client.js";

export const getAllPredictions = async () => {
    try {
        const predictions = await prisma.prediction.findMany();
        return predictions;
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
