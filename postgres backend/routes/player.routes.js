import { Router } from "express";
import { fetchAllPlayers, addPlayers, fetchAllPlayersFPLNames, fetchAllPlayersUnderstatNames, modifyPlayersUnderstatNames, removePlayerByFPLName } from "../controllers/player.controller.js";

const playerRouter = Router();

playerRouter.get("/", fetchAllPlayers);
playerRouter.post("/", addPlayers);

playerRouter.get("/fpl", fetchAllPlayersFPLNames);
playerRouter.delete("/fpl/:id", removePlayerByFPLName);

playerRouter.get("/understat", fetchAllPlayersUnderstatNames);
playerRouter.post("/understat", modifyPlayersUnderstatNames);

export default playerRouter;