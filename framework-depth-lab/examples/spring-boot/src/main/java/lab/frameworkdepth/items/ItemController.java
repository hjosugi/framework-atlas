package lab.frameworkdepth.items;

import jakarta.validation.Valid;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.server.ResponseStatusException;

@RestController
@RequestMapping
class ItemController {
    private final Map<Long, Item> items = new ConcurrentHashMap<>();
    private final AtomicLong sequence = new AtomicLong();

    @GetMapping("/healthz")
    Health health() {
        return new Health("ok");
    }

    @GetMapping("/items/{item_id}")
    Item getItem(@PathVariable("item_id") long itemId) {
        if (itemId < 1) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "item not found");
        }
        var item = items.get(itemId);
        if (item == null) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "item not found");
        }
        return item;
    }

    @PostMapping("/items")
    @ResponseStatus(HttpStatus.CREATED)
    Item createItem(@Valid @RequestBody CreateItem request) {
        var id = sequence.incrementAndGet();
        var item = new Item(id, request.name(), request.price());
        items.put(id, item);
        return item;
    }

    record Health(String status) {}

    record CreateItem(
            @NotBlank @Size(max = 100) String name,
            @NotNull @DecimalMin(value = "0.0", inclusive = true) Double price) {}

    record Item(long id, String name, double price) {}
}

record Problem(String code, String message) {}

@RestControllerAdvice
class ApiExceptionHandler {
    @ExceptionHandler(MethodArgumentNotValidException.class)
    ResponseEntity<Problem> validation(MethodArgumentNotValidException exception) {
        return ResponseEntity.unprocessableEntity()
                .body(new Problem("validation_error", "request validation failed"));
    }

    @ExceptionHandler(ResponseStatusException.class)
    ResponseEntity<Problem> status(ResponseStatusException exception) {
        return ResponseEntity.status(exception.getStatusCode())
                .body(new Problem("not_found", "item not found"));
    }
}
