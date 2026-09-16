SELECT
  id,
  first_name,
  last_name,
  email,
  birthdate
FROM
  `your-gcp-project-id.temp.customer_federated_tables`
WHERE
  birthdate >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 YEAR)
ORDER BY
  birthdate DESC
