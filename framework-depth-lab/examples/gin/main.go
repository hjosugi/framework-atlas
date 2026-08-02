package main

import (
	"net/http"
	"strconv"
	"sync"

	"github.com/gin-gonic/gin"
)

type createItem struct {
	Name  string   `json:"name" binding:"required,min=1,max=100"`
	Price *float64 `json:"price" binding:"required,gte=0"`
}

type item struct {
	ID    int64   `json:"id"`
	Name  string  `json:"name"`
	Price float64 `json:"price"`
}

type itemStore struct {
	mu    sync.RWMutex
	next  int64
	items map[int64]item
}

func newItemStore() *itemStore {
	return &itemStore{items: make(map[int64]item)}
}

func (s *itemStore) create(request createItem) item {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.next++
	created := item{ID: s.next, Name: request.Name, Price: *request.Price}
	s.items[created.ID] = created
	return created
}

func (s *itemStore) get(id int64) (item, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	result, ok := s.items[id]
	return result, ok
}

func newRouter() *gin.Engine {
	router := gin.New()
	router.Use(gin.Logger(), gin.Recovery())
	store := newItemStore()

	router.GET("/healthz", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})

	router.GET("/items/:item_id", func(c *gin.Context) {
		id, err := strconv.ParseInt(c.Param("item_id"), 10, 64)
		if err != nil || id < 1 {
			c.JSON(http.StatusNotFound, gin.H{"code": "not_found", "message": "item not found"})
			return
		}
		found, ok := store.get(id)
		if !ok {
			c.JSON(http.StatusNotFound, gin.H{"code": "not_found", "message": "item not found"})
			return
		}
		c.JSON(http.StatusOK, found)
	})

	router.POST("/items", func(c *gin.Context) {
		var request createItem
		if err := c.ShouldBindJSON(&request); err != nil {
			c.JSON(http.StatusUnprocessableEntity, gin.H{"code": "validation_error", "message": err.Error()})
			return
		}
		c.JSON(http.StatusCreated, store.create(request))
	})

	return router
}

func main() {
	if err := newRouter().Run(":8080"); err != nil {
		panic(err)
	}
}
