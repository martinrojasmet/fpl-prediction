import { Router } from "express";
import { getAllPredictions, getPredictionById, createPrediction, updatePrediction, deletePrediction } from "../controllers/prediction.controller.js";

const predictionRouter = Router();

predictionRouter.get("/", getAllPredictions);
predictionRouter.get("/:id", getPredictionById);
predictionRouter.post("/", createPrediction);
predictionRouter.put("/:id", updatePrediction);
predictionRouter.delete("/:id", deletePrediction);

export default predictionRouter;