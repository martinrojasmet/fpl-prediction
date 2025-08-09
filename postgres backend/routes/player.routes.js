import { Router } from "express";
import { fetchPlayers, addPlayers, fetchAllPlayersFPLNames, fetchAllPlayersUnderstatNames, modifyPlayersUnderstatNames, removePlayerByFPLName } from "../controllers/player.controller.js";

const playerRouter = Router();

playerRouter.get("/", fetchPlayers);
playerRouter.post("/", addPlayers);

playerRouter.get("/fpl", fetchAllPlayersFPLNames);
playerRouter.delete("/fpl/:id", removePlayerByFPLName);

playerRouter.get("/understat", fetchAllPlayersUnderstatNames);
playerRouter.post("/understat", modifyPlayersUnderstatNames);

export default playerRouter;