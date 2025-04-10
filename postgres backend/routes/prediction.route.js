import { Router } from "express";
import { fetchAllPredictions, addPrediction, modifyPrediction, removePrediction } from "../controllers/prediction.controller.js";

const predictionRouter = Router();

predictionRouter.get("/", fetchAllPredictions);
predictionRouter.post("/", addPrediction);
predictionRouter.put("/:id", modifyPrediction);
predictionRouter.delete("/:id", removePrediction);

export default predictionRouter;