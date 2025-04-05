import { Router } from "express";

const playerRouter = Router();

playerRouter.get("/", (req, res) => { res.send("Get all players") });
playerRouter.get("/:id", (req, res) => { res.send("Get player by ID") });
playerRouter.post("/", (req, res) => { res.send("Create a new player") });
playerRouter.post("/:id", (req, res) => { res.send("Update a player by ID") });
playerRouter.put("/:id", (req, res) => { res.send("Update a player by ID") });
playerRouter.delete("/:id", (req, res) => { res.send("Delete a player by ID") });

export default playerRouter;