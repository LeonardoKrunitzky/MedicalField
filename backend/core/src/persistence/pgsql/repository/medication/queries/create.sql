INSERT INTO medications (id,name, standard_dosage, created_at) VALUES (:id, :name, :standard_dosage, :created_at)
RETURNING *