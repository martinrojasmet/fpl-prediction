import { Router } from "express";
import { fetchPredictions, addPrediction, modifyPrediction, removePrediction } from "../controllers/prediction.controller.js";

const predictionRouter = Router();

predictionRouter.get("/", fetchPredictions);
predictionRouter.post("/", addPrediction);
predictionRouter.put("/:id", modifyPrediction);
predictionRouter.delete("/:id", removePrediction);

export default predictionRouter;