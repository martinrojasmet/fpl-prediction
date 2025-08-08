import { Router } from "express";
import { fetchAllGames, fetchGameById, addGames, modifyGame, removeGame } from "../controllers/game.controller.js";

const gameRouter = Router();

gameRouter.get("/", fetchAllGames);
gameRouter.get("/:id", fetchGameById);
gameRouter.post("/", addGames);
gameRouter.put("/:id", modifyGame);
gameRouter.delete("/:id", removeGame);

export default gameRouter;