PRAGMA foreign_keys = ON; -- esto lo habilito en cada conexion, para que
                          -- funcionen las foreign key

-- INSERT INTO Products(Code, Name, Price, EntryDate, Brand)
-- VALUES
--     ('P001', 'Mesa', 25000, '2024-12-10', 'IDK'),
--     ('P002', 'Silla', 12000, '2024-11-20', 'Star'),
--     ('P003', 'Sillon', 50000, '2024-12-05', 'Sony');

-- SELECT *
-- FROM Products

-- INSERT INTO Carts(Email)
-- VALUES 
--     ('jose.1@gmail.com'),
--     ('pedro.2@gmail.com');

-- INSERT INTO ProductCart(IdCart, IdProduct, Quantity)
-- VALUES 
--     (1, 11, 1),
--     (1, 12, 2);

-- INSERT INTO Invoices(InvoiceNumber, PurchaseDate, Email, Total, PhoneNumber, CodeEmployee)
-- VALUES
--     ('fac01', '2024-12-10', 'josue.ro@gmail.com', 174000, '85858585', 'emp01'),
--     ('fac02', '2024-12-11', 'ana.le@gmail.com', 112000, '60606060', 'emp01'),
--     ('fac03', '2024-11-9', 'luis.cr@gmail.com', 25000, '85508989', 'emp02');





-- INSERT INTO InvoiceDetail (IdInvoice, IdProduct, QuantityPurchased, TotalAmount)
-- VALUES
--     (1, 11, 2, 50000),
--     (1, 12, 1, 24000),
--     (1, 13, 2, 100000),
--     (2, 12, 1, 12000),
--     (2, 13, 2, 100000),
--     (3, 11, 1, 25000); 

