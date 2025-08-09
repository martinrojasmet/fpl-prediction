import { Router } from "express";
import { fetchGames, fetchGameById, addGames, modifyGame, removeGame } from "../controllers/game.controller.js";

const gameRouter = Router();

gameRouter.get("/", fetchGames);
gameRouter.get("/:id", fetchGameById);
gameRouter.post("/", addGames);
gameRouter.put("/:id", modifyGame);
gameRouter.delete("/:id", removeGame);

export default gameRouter;