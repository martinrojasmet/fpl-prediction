import { Router } from "express";
import { fetchAllDoubleGws, fetchDoubleGw, addDoubleGws, modifyDoubleGw, removeDoubleGw } from "../controllers/double_gw.controller.js";

const double_gwRouter = Router();

double_gwRouter.get("/", fetchAllDoubleGws);
double_gwRouter.get("/:gw", fetchDoubleGw);
double_gwRouter.post("/", addDoubleGws);
double_gwRouter.put("/:gw", modifyDoubleGw);
double_gwRouter.delete("/:gw", removeDoubleGw);

export default double_gwRouter;