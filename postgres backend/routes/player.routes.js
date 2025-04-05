import { Router } from "express";
import { getAllPlayers, getPlayerById, createPlayer, updatePlayer, deletePlayer } from "../controllers/player.controller.js";

const playerRouter = Router();

playerRouter.get("/", getAllPlayers);
playerRouter.get("/:id", getPlayerById);
playerRouter.post("/", createPlayer);
playerRouter.post("/:id", updatePlayer);
playerRouter.put("/:id", updatePlayer);
playerRouter.delete("/:id", deletePlayer);

export default playerRouter;