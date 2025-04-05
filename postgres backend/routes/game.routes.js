import { Router } from "express";

const gameRouter = Router();

gameRouter.get("/", (req, res) => { res.send("Get all games") });
gameRouter.get("/:id", (req, res) => { res.send("Get game by ID") });
gameRouter.post("/", (req, res) => { res.send("Create a new game") });
gameRouter.post("/:id", (req, res) => { res.send("Update a game by ID") });
gameRouter.put("/:id", (req, res) => { res.send("Update a game by ID") });
gameRouter.delete("/:id", (req, res) => { res.send("Delete a game by ID") });

export default gameRouter;