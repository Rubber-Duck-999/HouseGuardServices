db.createUser(
    {
        user: "root",
        pwd: "<password",
        roles: [
            {
                role: "readWrite",
                db: "house-guard"
            }
        ]
    }
);

db.createCollection('temperature', { capped: false });
db.createCollection('network', { capped: false });