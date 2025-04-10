import prisma from "../prisma/prisma-client";

export const getAllPredictions = async () => {
    try {
        const predictions = await prisma.prediction.findMany();
        return predictions;
    } catch (error) {
        throw new Error("Error retrieving predictions: " + error.message);
    }
}
