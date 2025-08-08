import { createPredictions } from "../services/prediction.service.js";

export const fetchAllPredictions = async (req, res) => {
    try {
        res.status(200).json({
            message: "Predictions retrieved successfully",
        });
    }
    catch (error) {
        next(error);
    }
};

export const addPrediction = async (req, res, next) => {
    try {
        const predictionsData = req.body.predictions;
        const result = await createPredictions(predictionsData);

        if (!result) {
            return res.status(400).json({
                message: "Failed to create prediction",
            });
        }

        res.status(201).json({
            message: "Prediction created successfully",
        });
    } catch (error) {
        next(error);
    }
};

export const modifyPrediction = async (req, res) => {
    try {
        res.status(200).json({
            message: "Prediction updated successfully",
        });
    } catch (error) {
        next(error);
    }
};

export const removePrediction = async (req, res) => {
    try {
        res.status(200).json({
            message: "Prediction deleted successfully",
        });
    } catch (error) {
        next(error);
    }
};