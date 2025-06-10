# endpoint POST books

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Crear un nuevo libro"""
    book = await BookService.create_book(db, book_data, current_user.id)
    return book

# método en book_service.py

@staticmethod
    async def create_book(db: AsyncSession, book_data: BookCreate, owner_id: int) -> Book:
        """Crear un nuevo libro"""
        db_book = Book(
            title=book_data.title,
            author=book_data.author,
            pages=book_data.pages,
            series_inspiration=book_data.series_inspiration,
            reading_status=book_data.reading_status or ReadingStatus.PENDIENTE,
            user_comments=book_data.user_comments,
            owner_id=owner_id
        )
        
        db.add(db_book)
        await db.commit()
        await db.refresh(db_book)
        return db_book
    
# schema

class BookResponse(BookBase):
    id: int
    reading_status: ReadingStatus
    user_comments: Optional[str] = None
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        
# modelo

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    author = Column(String(100), nullable=False)
    pages = Column(Integer, nullable=True)
    reading_status = Column(Enum(ReadingStatus), default=ReadingStatus.PENDIENTE, nullable=False)
    user_comments = Column(Text, nullable=True)
    series_inspiration = Column(Text, nullable=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign Key hacia User
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relación con usuario (muchos libros pertenecen a un usuario)
    owner = relationship("User", back_populates="books")
    