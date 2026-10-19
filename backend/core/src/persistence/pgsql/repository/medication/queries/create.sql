INSERT INTO medications (id,name, standard_dosage) VALUES (:id, :name, :standard_dosage)
RETURNING *