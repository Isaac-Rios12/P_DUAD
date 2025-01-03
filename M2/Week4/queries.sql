-- SELECT Books.BookID, Books.Name AS BookName, Authors.AuthorID, Authors.Name AS AuthorName
-- FROM Books
-- INNER JOIN Authors ON Books.Author = Authors.AuthorID

-- SELECT * 
-- FROM Books
-- WHERE Author is NULL


-- SELECT *
-- FROM Authors
-- LEFT JOIN Books ON Authors.AuthorID = Books.Author
-- WHERE Books.BookID IS NULL


-- SELECT DISTINCT Books.BookID, Books.Name, COUNT(*) AS RentCount
-- FROM Rents
-- JOIN Books ON Rents.BookID = Books.BookID
-- GROUP BY Books.BookID;


-- SELECT *
-- FROM Books
-- LEFT JOIN Rents ON Books.BookID = Rents.BookID
-- WHERE Rents.RentID IS NULL

-- SELECT * 
-- FROM Customers
-- LEFT JOIN Rents ON Customers.CustomerID = Rents.CustomerID
-- WHERE Rents.RentID IS NULL

SELECT Books.Name, Rents.State
FROM Books
INNER JOIN Rents ON Books.BookID = Rents.BookID
WHERE STATE IS "Overdue"