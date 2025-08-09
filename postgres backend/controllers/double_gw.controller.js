import { getDoubleGws, getDoubleGwByGw, createDoubleGws, updateDoubleGw, deleteDoubleGw } from "../services/double_gw.service.js";

export const fetchDoubleGws = async (req, res, next) => {
    try {
        const { cursor, limit, ...filters } = req.query;
        const result = await getDoubleGws(filters, cursor, limit);
        
        if (!result.data || result.data.length === 0) {
            return res.status(404).json({
                message: "No double gameweeks found",
            });
        }

        res.status(200).json({
            message: "Double gameweeks retrieved successfully",
            data: result.data,
            nextCursor: result.nextCursor
        });
    } catch (error) {
        next(error);
    }
};

export const fetchDoubleGw = async (req, res, next) => {
    try {
        const gw = req.params.gw;
        const doubleGw = await getDoubleGwByGw(gw);

        if (!doubleGw || doubleGw.length === 0) {
            return res.status(404).json({
                message: "Double gameweek not found"
            });
        }

        res.status(200).json({
            message: "Double gameweek retrieved successfully",
            data: doubleGw,
        });
    } catch (error) {
        next(error);
    }
};

export const addDoubleGws = async (req, res, next) => {
    try {
        const doubleGwsData = req.body.doubleGWs;
        const result = await createDoubleGws(doubleGwsData);

        if (!result) {
            return res.status(400).json({
                message: "Failed to create double gameweeks",
            });
        }

        res.status(201).json({
            message: "Double gameweeks created successfully",
            data: result
        });
    } catch (error) {
        next(error);
    }
};

export const modifyDoubleGw = async (req, res, next) => {
    try {
        const gw = req.params.gw;
        const doubleGwData = req.body.data;
        const result = await updateDoubleGw(gw, doubleGwData);

        if (!result) {
            return res.status(400).json({
                message: "Failed to update double gameweek",
            });
        }

        res.status(200).json({
            message: "Double gameweek updated successfully",
        });
    } catch (error) {
        next(error);
    }
};

export const removeDoubleGw = async (req, res, next) => {
    try {
        const gw = req.params.gw;
        const result = await deleteDoubleGw(gw);

        if (!result) {
            return res.status(400).json({
                message: "Failed to delete double gameweek",
            });
        }

        res.status(200).json({
            message: "Double gameweek deleted successfully",
        });
    } catch (error) {
        next(error);
    }
};