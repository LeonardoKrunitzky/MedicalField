INSERT INTO patients (id, name, document, created_at)
VALUES(:id, :name, :document, :created_at)
RETURNING *;