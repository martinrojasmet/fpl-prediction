const errorMiddleware = (err, req, res, next) => {
    try {
        let error = { ... err };

        error.message = err.message;

        console.log(err);

        res.status(error.statusCode || 500).json({
            error: {
                code: error.code || "ERR_INTERNAL",
                message: error.message || "Internal Server Error",
                details: error.details || [
                    {
                        field: "unknown",
                        issue: error.issue || "An unknown error occurred",
                    },
                ]
            }
        });
    } catch (error) {
        next(error);
    }
};

export default errorMiddleware;