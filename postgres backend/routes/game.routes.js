import { Router } from "express";
import { getAllGames, getGameById, createGame, updateGame, deleteGame } from "../controllers/game.controller.js";

const gameRouter = Router();

gameRouter.get("/", getAllGames);
gameRouter.get("/:id", getGameById);
gameRouter.post("/", createGame);
gameRouter.post("/:id", updateGame);
gameRouter.put("/:id", updateGame);
gameRouter.delete("/:id", deleteGame);

export default gameRouter;