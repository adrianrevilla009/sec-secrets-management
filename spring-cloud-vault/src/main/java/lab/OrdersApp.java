package lab;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class OrdersApp {
    public static void main(String[] args) {
        SpringApplication.run(OrdersApp.class, args);
    }

    /** The value comes from Vault KV (secret/orders-app), not from any file in this repo. */
    @Bean
    CommandLineRunner show(@Value("${orders.db.password}") String password) {
        return args -> System.out.println("Loaded secret from Vault, length=" + password.length());
    }
}
