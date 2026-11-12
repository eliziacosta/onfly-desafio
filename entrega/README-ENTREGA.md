# Entrega — Consolidador de reservas de hotel

## Defeitos corrigidos

| 1 | `repositories/csv_reservation_repository.py` | Só as 200 primeiras reservas eram lidas (o CSV real tem 300) | Havia um `break` ao atingir 200 linhas, truncando a leitura silenciosamente. |
| 2 | `services/status_policy.py` | `NO_SHOW` entrava em noites, valores, `by_month` e `top_hotels` | `is_billable` retornava `status != "CANCELLED"` em vez de `status == "CONFIRMED"`. |
| 3 | `services/stay_calculator.py` | Noites erradas na virada de mês/ano | Subtraía `checkout.day - checkin.day` (dia do mês) em vez da diferença entre datas. |
| 4 | `services/currency_converter.py` | Valores em USD/EUR errados e com imprecisão de float | Dividia por `rate_to_brl` e passava por `float`; o correto é `amount * rate` em `Decimal`. |
| 5 | `services/report_builder.py` | `top_hotels` vinha do menor para o maior valor | Ordenava por `amount` crescente; o correto é `-amount` com desempate por `hotel_id` crescente. |

## Como investiguei

1. Li o README (regras e contrato) e todo o código do CLI.
2. Comparei cada regra do README com a função correspondente, o que revelou os defeitos 2 a 5.
3. O defeito 1 não era coberto por nenhum teste: percebi ao conferir que o CSV real tem 300 reservas. Confirmei após a correção (`total_reservations = 300`).
4. Rodei a amostra `data/exemplo-validacao.csv` e comparei com a tabela do README.
5. Adicionei `tests/test_extra_regressions.py` para os cenários não cobertos.

Os testes fornecidos não foram alterados.

## Como validar

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q

PYTHONPATH=src python -m onfly_report \
  --input data/exemplo-validacao.csv --rates data/taxas_cambio.csv --output output/exemplo.json
PYTHONPATH=src python -m onfly_report \
  --input data/reservas_hoteis.csv --rates data/taxas_cambio.csv --output output/report.json
```

## Resultado

- Amostra: 12 / 9 / 2 / 1 reservas, 28 noites, `7566.00` BRL, média `270.21`, igual ao README.
- Dataset completo: 300 reservas, 235 confirmadas, 1347 noites, `396170.00` BRL.
- `pytest -q`: **11 passed** (5 fornecidos + 6 adicionais).
