WITH RECURSIVE mortgage AS (

    SELECT
        1 AS month,
        :principal AS opening_balance,
        :payment AS payment,
        :principal * (:rate / 12.0) AS interest,
        :payment - (:principal * (:rate / 12.0)) AS principal_paid,
        :principal
            - (:payment - (:principal * (:rate / 12.0)))
            AS closing_balance

    UNION ALL

    SELECT
        month + 1,
        closing_balance,
        :payment,
        closing_balance * (:rate / 12.0),
        :payment - (closing_balance * (:rate / 12.0)),
        closing_balance
            - (:payment - (closing_balance * (:rate / 12.0)))

    FROM mortgage

    WHERE month < :months
      AND closing_balance > 0
)

SELECT *
FROM mortgage;