import { Router } from "express";
import { fetchAllGames, fetchGameById, addGame, modifyGame, removeGame } from "../controllers/game.controller.js";

const gameRouter = Router();

gameRouter.get("/", fetchAllGames);
gameRouter.get("/:id", fetchGameById);
gameRouter.post("/", addGame);
gameRouter.put("/:id", modifyGame);
gameRouter.delete("/:id", removeGame);

export default gameRouter;