import { Router } from "express";
import { getAllFixtures, getFixtureById, createFixture, updateFixture, deleteFixture } from "../controllers/fixture.controller.js";

const fixtureRouter = Router();

fixtureRouter.get("/", getAllFixtures);
fixtureRouter.get("/:id", getFixtureById);
fixtureRouter.post("/", createFixture);
fixtureRouter.post("/:id", updateFixture);
fixtureRouter.put("/:id", updateFixture);
fixtureRouter.delete("/:id", deleteFixture);

export default fixtureRouter;