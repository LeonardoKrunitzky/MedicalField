INSERT INTO patients (id, name, document)
VALUES(:id, :name, :document)
RETURNING *;