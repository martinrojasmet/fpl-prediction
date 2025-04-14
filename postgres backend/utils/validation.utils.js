export const parseValueByType = (fieldType, value, fieldName) => {
    switch (fieldType) {
        case 'Int':
            const intValue = parseInt(value, 10);
            if (isNaN(intValue)) {
                throw new Error(`'${fieldName}' must be an integer (received: ${value})`);
            }
            return intValue;
        
        case 'DateTime':
            const dateValue = new Date(value);
            if (isNaN(dateValue.getTime())) {
                throw new Error(`'${fieldName}' must be a valid ISO date string (received: ${value})`);
            }
            return dateValue;
        
        case 'Boolean':
            if (value === 'true') return true;
            if (value === 'false') return false;
            throw new Error(`'${fieldName}' must be 'true' or 'false' (received: ${value})`);
        
        case 'String':
            return String(value);

        case 'Float':
            const floatValue = parseFloat(value);
            if (isNaN(floatValue)) {
                throw new Error(`'${fieldName}' must be a float (received: ${value})`);
            }
            return floatValue;
        
        default:
            return value;
    }
};