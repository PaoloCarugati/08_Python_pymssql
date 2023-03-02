CREATE PROCEDURE dbo.PC_InserisciPost
  @Autore varchar(50),
  @Testo varchar(255),
  @Identity int OUT
AS

BEGIN
	INSERT INTO PC_FB_Post (Autore, Testo) VALUES (@Autore, @Testo)
	SET @Identity = SCOPE_IDENTITY()
END