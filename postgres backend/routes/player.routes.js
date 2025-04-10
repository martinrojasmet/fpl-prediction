import { Router } from "express";
import { fetchAllPlayers, addPlayer, modifyPlayer, removePlayer } from "../controllers/player.controller.js";

const playerRouter = Router();

playerRouter.get("/", fetchAllPlayers);
playerRouter.post("/", addPlayer);
playerRouter.put("/:id", modifyPlayer);
playerRouter.delete("/:id", removePlayer);

export default playerRouter;