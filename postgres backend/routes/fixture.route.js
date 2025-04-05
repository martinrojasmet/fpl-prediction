import { Router } from "express";

const fixtureRouter = Router();

fixtureRouter.get("/", (req, res) => { res.send("Get all fixtures"); });
fixtureRouter.get("/:id", (req, res) => { res.send("Get fixture by ID"); });
fixtureRouter.post("/", (req, res) => { res.send("Create a new fixture"); });
fixtureRouter.post("/:id", (req, res) => { res.send("Update a fixture by ID"); });
fixtureRouter.put("/:id", (req, res) => { res.send("Update a fixture by ID"); });
fixtureRouter.delete("/:id", (req, res) => { res.send("Delete a fixture by ID"); });

export default fixtureRouter;