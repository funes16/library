-- Estructura de tabla para la tabla `books`
CREATE TABLE `books` (
  `ID` int(11) NOT NULL,
  `CODE` varchar(3) NOT NULL,
  `NAME` varchar(255) NOT NULL,
  `AUTHOR` varchar(255) NOT NULL,
  `GENRE` varchar(255) NOT NULL,
  `PUBLICATION_DATE` date NOT NULL,
  `CREATE_DATE` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Indices de la tabla `books`
ALTER TABLE `books`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `UNIQUE_NAME` (`NAME`),
  ADD UNIQUE KEY `UNIQUE_CODE` (`CODE`) USING BTREE,
  ADD KEY `IDX_ID` (`ID`) USING BTREE;

-- AUTO_INCREMENT de la tabla `books`
ALTER TABLE `books`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;
