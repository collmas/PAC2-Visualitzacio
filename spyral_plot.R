library(ggplot2)
library(dplyr)

# Carreguem el csv
df <- read.csv("/Users/collm/Documents/master/GitHub/PAC2-Visualitzacio/data/muertos_en_accidentes_de_trafico_en_los_ultimos_10_años.csv", sep=";") %>% 
  filter(Año > 2014)

# Afegim el numèrics per mes i any
df$num_mes <- rep(1:12, length(unique(df$Año)))[1:length(df$Periodo)]
df$num_any <- factor(rep(1:length(unique(df$Año)), length(unique(df$Periodo)), each=12)[1:length(df$Periodo)])

# Afegim també les alçades que hagin de tenir les entrades
df$y <- as.numeric(df$num_any) - 1 + (df$num_mes - 1) / 12

barres <- df %>% 
  mutate(value_norm = Víctimas.mortales / (max(Víctimas.mortales) * 1.1),
         xmin = num_mes - 0.5,
         xmax = num_mes + 0.5,
         ymin = y,
         ymax = y + value_norm,
         victimas = Víctimas.mortales)

poligons <- barres %>% 
  rowwise() %>% 
  do(with(., tibble(year = Año,
                        month = Periodo,
                        x = c(xmin, xmax, xmax, xmin),
                        y = c(ymin - 1/24, 
                              ymin + 1/24, 
                              ymax + 1/24, 
                              ymax - 1/24),
                        value = victimas)))

dates_text <- data.frame(
  x_date = c(12.1, 9.63, 3, 6),
  y_date = c(0.4, 10.1, 11, 11),
  label_date = c("2015", "2024", "Inici Confinament", "Fi Confinament"),
  angle = c(0, 90, 285, 0),
  size = c(2.5, 2.5, 2, 2)
)

mesos_cat <- c("Gener", "Febrer", "Març", "Abril", 
               "Maig", "Juny", "Juliol", "Agost",
               "Setembre", "Octubre", "Novembre", "Desembre")


# Gradient vermell-blanc
ggplot(poligons, aes(x = x, y = y)) + 
  geom_polygon(color = "#FFFFFF", aes(fill = value, group = interaction(month, year))) +
  coord_polar() +
  ylim(-3, 11) +
  scale_fill_gradient(low = "white", high = "red", name = "Morts") + 
  scale_x_continuous(breaks = 1:12, labels = mesos_cat) +
  theme_minimal()+ 
  geom_text(data=dates_text, aes(x=x_date, y=y_date, label=label_date), 
            color="black", size=dates_text$size, fontface="bold", angle=dates_text$angle) + 
  labs(title = "Morts en accidents de trànsit dels últims 10 anys a Espanya",
       subtitle = "(a nivell mensual)") + 
  theme(legend.position = "right", axis.text.y = element_blank(),
        plot.title = element_text(hjust = 0.5), axis.title = element_blank(),
        legend.title = element_text(size=8), legend.text = element_text(size=6),
        plot.subtitle = element_text(hjust = 0.5), panel.grid.major = element_blank(), panel.grid.minor = element_blank()) +
  annotate("segment", x = 3, xend = 3, y = 5.5, yend = 10.6, colour = "#AAAAAA", size=0.5, alpha=1, arrow=arrow(type="closed", length=unit(0.2, "cm"))) +
  annotate("segment", x = 6, xend = 6, y = 5.75, yend = 10.75, colour = "#AAAAAA", size=0.5, alpha=1, arrow=arrow(type="closed", length=unit(0.2, "cm")))


