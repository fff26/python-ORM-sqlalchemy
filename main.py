from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float, create_engine, and_, or_
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    books = relationship("Book", back_populates="publisher")


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))

    publisher_id = Column(Integer, ForeignKey('publisher.id'))
    publisher = relationship("Publisher", back_populates="books")

    stocks = relationship("Stock", back_populates="book")


class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    stocks = relationship("Stock", back_populates="shop")


class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    count = Column(Integer)

    book_id = Column(Integer, ForeignKey('book.id'))
    book = relationship("Book", back_populates="stocks")

    shop_id = Column(Integer, ForeignKey('shop.id'))
    shop = relationship("Shop", back_populates="stocks")

    sales = relationship("Sale", back_populates="stock")


class Sale(Base):
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    date_sale = Column(DateTime)
    count = Column(Integer)

    stock_id = Column(Integer, ForeignKey('stock.id'))
    stock = relationship("Stock", back_populates="sales")


if __name__== '__main__':
    # Подключение к базе данных PostgreSQL
    engine = create_engine('postgresql://user:password@host:port/database')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Ввод имени или id издателя
    publisher_name = input("Введите имя или идентификатор издателя: ")

    # Поиск издателя
    publisher = session.query(Publisher).filter(
    or_(
        Publisher.id == publisher_name,
        Publisher.name == publisher_name
    )
    ).first()

    # Проверка, найден ли издатель
    if publisher is None:
        print(f"Издатель с именем или идентификатором '{publisher_name}' не найден.")
    else:
        # Выборка магазинов, продающих книги издателя
        shops = session.query(Shop).join(Shop.stocks).join(Stock.book).filter(
            and_(
                Book.publisher_id == publisher.id,
                Sale.stock_id == Stock.id
            )
        ).all()

    # Вывод результатов
    for shop in shops:
        sales = session.query(Sale).join(Sale.stock).join(Stock.book).join(Book.publisher).filter(
            and_(
                Shop.id == shop.id,
                Book.publisher_id == publisher.id
            )
        ).all()

        for sale in sales:
            print(f"{sale.stock.book.title} | {shop.name} | {sale.price} | {sale.date_sale.strftime('%d-%m-%Y')}")
